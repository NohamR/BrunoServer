"""Flask server for license activation and verification."""
from datetime import datetime
import os
import uuid
import json
import base64

from flask import Flask, jsonify, request


app = Flask(__name__)

PENDING_ACTIVATIONS = {}

def _b64url_encode(data: bytes) -> str:
    """Base64 URL-safe encode data."""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _make_jwt_like(payload: dict) -> str:
    """Create a JWT-like token."""
    header = {"alg": "HS256", "typ": "JWT"}
    header_json = json.dumps(header, separators=(",", ":"),
                             ensure_ascii=False).encode("utf-8")
    header_b64 = _b64url_encode(header_json)
    payload_json = json.dumps(payload, separators=(",", ":"),
                              ensure_ascii=False).encode("utf-8")
    payload_b64 = _b64url_encode(payload_json)
    signature_b64 = _b64url_encode(b"signature")
    return f"{header_b64}.{payload_b64}.{signature_b64}"


@app.route("/api/v2/license/activate", methods=["POST"])
def activate_license():
    """Handle license activation request."""
    payload = request.get_json(silent=True) or {}
    print("Received activation request:", payload)

    license_key = payload.get("licenseKey", "")
    device_id = payload.get("deviceId", str(uuid.uuid4()))
    device_name = payload.get("deviceName", "Unnamed Device")
    email = payload.get("email")
    license_server_url = payload.get("licenseServerUrl")

    activation_id = str(uuid.uuid4())
    activated_at = datetime.utcnow().isoformat() + "Z"

    PENDING_ACTIVATIONS[activation_id] = {
        "licenseKey": license_key,
        "deviceId": device_id,
        "deviceName": device_name,
        "email": email,
        "licenseServerUrl": license_server_url,
        "activatedAt": activated_at,
    }

    resp = {
        "status": "activated",
        "licenseKey": license_key,
        "deviceId": device_id,
        "deviceName": device_name,
        "email": email,
        "activationId": activation_id,
        "activatedAt": activated_at,
    }

    return jsonify(resp), 200


@app.route("/api/v1/license/activate/<activation_id>", methods=["POST"])
def verify_activation_otp(activation_id: str):
    """Verify activation OTP and return license token."""
    payload = request.get_json(silent=True) or {}
    print("Received OTP verification:",
          {"activationId": activation_id, **payload})

    pending = PENDING_ACTIVATIONS.get(activation_id)
    if not pending:
        return jsonify({"error": "Invalid activationId"}), 404

    now_iso = datetime.utcnow().isoformat() + "Z"
    license_payload = {
        "licenseKey": pending.get("licenseKey"),
        "email": pending.get("email"),
        "deviceId": pending.get("deviceId"),
        "deviceName": pending.get("deviceName"),
        "licenseServerUrl": pending.get("licenseServerUrl"),
        # ["PRO_EDITION","GOLDEN_EDITION","ULTIMATE_EDITION"]
        "plan": "ULTIMATE_EDITION",
        "type": "personal",
        "createdAt": pending.get("activatedAt"),
        "updatedAt": now_iso,
        "trialActive": False,
    }

    token = _make_jwt_like(license_payload)
    PENDING_ACTIVATIONS.pop(activation_id, None)

    return jsonify({
        "licenseToken": token,
    }), 200


@app.route("/api/v2/license/verify", methods=["POST"])
def verify_license():
    """Verify license token."""
    payload = request.get_json(silent=True) or {}
    print("Received license verification:", payload)

    response = {
        "verified": True,
        "subscription": {
            "plan": "ULTIMATE_EDITION"
        }
    }

    return jsonify(response), 200


def create_app():
    """Create and return Flask app."""
    return app


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host=host, port=port, debug=debug)
