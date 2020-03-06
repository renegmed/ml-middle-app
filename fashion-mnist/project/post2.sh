
export URL='http://localhost:8000'
export PIC='images/meters2.jpeg'  # working
export PIC_1='images/24.jpg'    # working
export PIC_2='images/57.jpg'    # working
export PIC_3='images/bubble_red_dress.jpeg'  # working
export PIC_4='images/black_ankle_boot.jpg' # working
export ENDPOINT_NAME='fake_endpoint'

#(echo '{"data": "'; base64 $PIC; echo '", "height": 28 , "width": 28}') | curl -X POST -H "Content-Type: application/json" -d @-  $URL

curl -X POST -H 'Accept: image/jpeg' -H 'Content-Type: image/jpeg' --data-binary @$PIC_3 $URL  