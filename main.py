from flask import Flask, jsonify, request

app = Flask(__name__)

server_cache = {"value": 0}

BIT_LENGTH = 8 # default is 8 btw

PASSWORD = "1234"  # put with ur password here

@app.route('/', methods=["GET", "POST"])  #dw about it
def main():
    if request.method == "POST":
        password = request.headers.get("Password")
        if password != PASSWORD:
            return jsonify({"error": "unauthorized. invalid password."}), 401

        value = request.form.get("value")
        if value:
            try:
                # trying to parse as integer first
                int_value = int(value)
                # checking if fits in the bit length
                if 0 <= int_value < (2**BIT_LENGTH):
                    server_cache["value"] = int_value
                    return jsonify({
                        "value":
                        format(server_cache["value"], f'0{BIT_LENGTH}b')
                    }), 200
                else:
                    return jsonify({
                        "error":
                        f"value must be between 0 and {(2 ** BIT_LENGTH) - 1}."
                    }), 400
            except ValueError:
                # if is not an integer, script gonna try parsing as binary
                if len(value) == BIT_LENGTH and all(c in "01" for c in value):
                    server_cache["value"] = int(value, 2)
                    return jsonify({
                        "value":
                        format(server_cache["value"], f'0{BIT_LENGTH}b')
                    }), 200
                else:
                    return jsonify({
                        "error":
                        f"invalid value. must be an integer (0-{(2 ** BIT_LENGTH) - 1}) or {BIT_LENGTH}-bit binary string."
                    }), 400

        return jsonify({"error": "no value provided."}), 400

    elif request.method == "GET":
        return jsonify(
            {"value": format(server_cache["value"], f'0{BIT_LENGTH}b')}), 200


if __name__ == '__main__':
    import threading

    # starting the server
    server_thread = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=5000, debug=False))
    server_thread.daemon = True
    server_thread.start()

    print("server started on port 5000")
    print(
        f"current value: {format(server_cache['value'], f'0{BIT_LENGTH}b')} (decimal: {server_cache['value']})"
    )
    print(f"enter values (0-{(2 ** BIT_LENGTH) - 1}):")

    while True:
        try:
            user_input = input("> ").strip()

            if user_input == '':
                continue

            # checking for password
            if ":" in user_input:
                parts = user_input.split(":", 1)
                if len(parts) == 2:
                    input_password, value_part = parts
                    if input_password != PASSWORD:
                        print("unauthorized. invalid password.")
                        continue
                    user_input = value_part
                else:
                    print("input is not a number, enter a new value")
                    continue

            # checking if input is contains only digits
            if not user_input.isdigit():
                print("input is not a number, enter a new value")
                continue

            # iflength > 3 or starts with 0, try as binary first
            if len(user_input) > 3 or user_input[0] == "0":
                try:
                    value = int(user_input, 2)
                except:
                    value = int(user_input)
            else:
                value = int(user_input)

            # check if value exceeds maximum
            if value > (2**BIT_LENGTH) - 1:
                print(
                    f"input value is too large (max {(2 ** BIT_LENGTH) - 1})")
                continue
            else:
                server_cache["value"] = value
                print(
                    f"value set to: {format(server_cache['value'], f'0{BIT_LENGTH}b')} (decimal: {server_cache['value']})"
                )
                continue
        except KeyboardInterrupt:
            break
        except EOFError:
            break
