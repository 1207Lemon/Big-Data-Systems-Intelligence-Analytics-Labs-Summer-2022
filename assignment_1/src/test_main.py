from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_inputInfoFilterRequest():
    response = client.get("/api/get/infoFilter/?filename=0cd99a9ee135c7618006540f5b6d9b1b")
    assert response.status_code == 200
    assert response.json() == {
        "53": {
    "filename": "0cd99a9ee135c7618006540f5b6d9b1b",
    "width": "1079",
    "height": "1600",
    "class": "F16",
    "xmin": "77",
    "ymin": "263",
    "xmax": "950",
    "ymax": "658"
  }
    }

def test_aircraftClassAndFileNameRequest():
    response = client.get("/api/get/fileNameAndClass/?className=F16")
    assert response.status_code == 200

def test_no_found_aircraftClassAndFileNameRequest():
    response = client.get("/api/get/fileNameAndClass/?className=F10")
    assert response.status_code == 200
    assert response.json() == {}

def test_no_found_imgSzieRangeRequest():
    response = client.get("/api/get/imgSizeRange/?width=500&height=500")
    assert response.status_code == 200
    assert response.json() == {}

def test_incorrect_input_imgSzieRangeRequest():
    response = client.get("/api/get/imgSizeRange/?width=abc&height=500")
    assert response.status_code == 422

def test_imgSzieRangeRequest():
    response = client.get("/api/get/imgSizeRange/?width=500")
    assert response.status_code == 200
    assert response.json() == {
        "211": {
    "filename": "2facce0cb214667e67f9f742682df922",
    "width": "436",
    "height": "600",
    "class": "YF23",
    "xmin": "49",
    "ymin": "376",
    "xmax": "304",
    "ymax": "546"
  },
  "212": {
    "filename": "2facce0cb214667e67f9f742682df922",
    "width": "436",
    "height": "600",
    "class": "YF23",
    "xmin": "129",
    "ymin": "29",
    "xmax": "386",
    "ymax": "169"
  }
    }

def test_numAndClassFiteredInfoRequest():
    response = client.get("/api/get/aircraftNumandClass/?num=5&className=F16")
    assert response.status_code == 200
    assert response.json() == {
        "133": {
    "filename": "4a042db1cef213a1ed865422e6355f76",
    "class": "F16",
    "count": 5
  }
    }

def test_aircraftPositionRequest():
    response = client.get("/api/get/aircraftPositionRange/?xmin=500&ymin=500&xmax=900&ymax=900")
    assert response.status_code == 200
    assert response.json() == {
        "131": {
    "filename": "1deecbebb637c7cfcb1ed6ef993243c1",
    "width": "1500",
    "height": "969",
    "class": "JAS39",
    "xmin": "616",
    "ymin": "672",
    "xmax": "704",
    "ymax": "731"
  },
  "175": {
    "filename": "2cc2da26e5c852e86339633fdffccbba",
    "width": "1600",
    "height": "1596",
    "class": "Rafale",
    "xmin": "509",
    "ymin": "713",
    "xmax": "630",
    "ymax": "856"
  },
  "299": {
    "filename": "4ef3fc177420d40c4a714f74fc370d41",
    "width": "2048",
    "height": "1365",
    "class": "V22",
    "xmin": "594",
    "ymin": "616",
    "xmax": "699",
    "ymax": "668"
  }
    }