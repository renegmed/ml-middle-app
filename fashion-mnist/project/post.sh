
export URL='http://localhost:8000'
export PIC='meters2.jpeg'
export ENDPOINT_NAME='fake_endpoint'

(echo '{"data": "'; base64 $PIC; echo '", "height": 28 , "width": 28}') | curl -X POST -H "Content-Type: application/json" -d @-  $URL


