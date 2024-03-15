from flask import jsonify

class ApiResponse:
    @staticmethod
    def success(data=None, code=0):
        response = {"status": "success", "code": code}
        if data is not None:
            response["data"] = data
        return jsonify(response)

    @staticmethod
    def error(message, code=1):
        response = {"status": "error", "code": code, "message": message}
        return jsonify(response)
