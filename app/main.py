import os
from flask import Flask, request, jsonify
from db.db import SessionLocal
from db.models import User, Session
from pyngrok import ngrok
from datetime import datetime
from ipaddress import ip_address
import uuid

app = Flask(__name__)

def convert_timestamp(ts):
    """
    converted Clerk's millisecond timestamps to datetime
    """
    if ts:
        return datetime.fromtimestamp(ts/1000)
    return None

@app.route("/webhooks/clerk", methods=["POST"])
def clerk_webhook():
    try:
        data = request.json
        print("=== Incoming Webhook ===")
        print(data)   # 👈 log the raw Clerk payload
        event_type = data.get("type")
        event_type = data.get("type")
        print("Event Type:", event_type)
        if event_type == "user.created":
            attributes = data["data"]
            clerk_id = attributes["id"]
            email_obj = attributes["email_addresses"][0]
            email = email_obj["email_address"]
            email_verified = email_obj["verification"]["status"] == "verified"
            image_url = attributes.get("image_url") or attributes.get("profile_image_url")
            
            
            created_at = convert_timestamp(attributes.get("created_at"))
            updated_at = convert_timestamp(attributes.get("updated_at"))
            
            session = SessionLocal()
            user = User(
                clerk_id=clerk_id,
                email=email,
                email_verified=email_verified,
                image=image_url,
                created_at=created_at,
                updated_at=updated_at,
            )
            session.add(user)
            session.commit()
            session.close()
            return jsonify({"status": "user created", "clerk_id": clerk_id}), 200
        elif event_type == "user.deleted":
            clerk_id = data["data"]["id"]
            session = SessionLocal()
            user = session.query(User).filter(User.clerk_id == clerk_id).first()
            if user:
                session.delete(user)
                session.commit()
            session.close()
            return jsonify({"status": "user deleted", "clerk_id": clerk_id}), 200
        # session created user login
        elif event_type == "session.created":
            attributes = data["data"]
            session_id = attributes["id"]
            user_id = attributes["user_id"]
            expires_at = convert_timestamp(attributes.get("expire_at"))
            
            ip_address = data.get("event_attributes", {}).get("http_request", {}).get("client_ip")
            user_agent = data.get("event_attributes", {}).get("http_request", {}).get("user_agent")
            
            db = SessionLocal()
            user = db.query(User).filter(User.clerk_id == user_id).first()
            
            if user:
                new_session = Session(
                    id = session_id,
                    user_id = user.id,
                    expires_at=expires_at,
                    token=str(uuid.uuid4()),  # placeholder until we generate JWT
                    ip_address=ip_address,
                    user_agent=user_agent,
                )
                db.add(new_session)
                db.commit()
                print("✅ Session created for user:", user.email)
            db.close()
            return jsonify({"status": "session created", "session_id": session_id}), 200
        elif event_type == "session.removed":
            session_id = data["data"]["id"]
            
            db = SessionLocal()
            s = db.query(Session).filter(Session.id == session_id).first()
            if s:
                db.delete(s)
                db.commit()
                print("Session ended: ", session_id)
            db.close()
            return jsonify({"status": "session ended", "session_id": session_id}), 200
        return jsonify({"status": "ignored"}), 200
    except Exception as e:
        print("❌ Error in webhook:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return {"message": "Flask backend is running!"}, 200

if __name__ == "__main__":
    # Open an ngrok tunnel to port 5000
    public_url = ngrok.connect(5000)
    print(" * ngrok tunnel:", public_url)
    app.run(port=5000)