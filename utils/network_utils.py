import socket
import qrcode
from io import BytesIO


def get_local_ip() -> str:
    """
    get the local IP address of the machine.
    
    returns:
        String containing the local IP address, or empty string if not found
    """
    try:
        # start a socket t
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # udp is connectionless
        s.connect(("8.8.8.8", 80))
        # get the local IP address bound to socket
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            # alternative: get hostname and translate to IP
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception:
            return ""


def generate_qr_code(data):
    """
    generate a qr code from the given data.
    returns:
        qr code
    """
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()