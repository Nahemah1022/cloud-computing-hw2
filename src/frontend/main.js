var encoded = null;
var filename = null;
var API_KEY = "0wwl2gc2cI4JAojQeWcFMjvoX7eCW7KoLUKPoy10"

window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
const synth = window.speechSynthesis;
const recognition = new SpeechRecognition();
recognition.continuous = true;

recognition.onerror = (e) => {
    console.log("something went wrong");
    console.log(e);
};

recognition.onend = () => {
    console.log("ended");
};
  
window.onload = function () {
    $("#upload_files").change(function(e) {
        for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {
    
            var file = e.originalEvent.srcElement.files[i];
            filename = file.name
    
            var img = document.createElement("img"); // create an image element
            var reader = new FileReader();
            reader.onloadend = function() {
                img.src = reader.result; // attach file content to the created image element's src for display
                encoded = img.outerHTML;
                // var data=(reader.result).split(',')[1];
                // var binaryBlob = atob(data); // convert file content to binary for PUT
                // console.log('Encoded Binary File String:', binaryBlob);
            }
            reader.readAsDataURL(file);
            $(".upload-inputs").after(img);
        }
    });

    $('#query_btn').click(function (event) {
        event.preventDefault();
        var query = $('#query_txt').val();
        axios.get(
            `https://zw6zd19ubb.execute-api.us-east-2.amazonaws.com/dev/cloud.uploadtest?myQuery=${query}`, 
            {
                headers: {
                    'x-api-key': API_KEY
                }
            }
        ).then((response) => {
            var results = response.data.body;

            for (let i=0; i<results.length; ++i) {
                console.log(results[i]['label'])
                let frame = document.createElement("div");
                frame.classList.add('frame');
                let img = document.createElement("img");
                let banner = document.createElement("div");
                banner.classList.add('banner');
                results[i]['label'] = [...new Set(results[i]['label'])]
                results[i]['label'].forEach(label => {
                    let span = document.createElement("span");
                    span.innerText = label;
                    banner.appendChild(span);
                });

                let url = results[i]['url'];
                fetch(url).then((res) => {
                    return res.text();
                }).then((data) => {
                    img.src = `data:image/jpeg;base64,${data}`;
                })
                frame.appendChild(banner);
                frame.appendChild(img);
                $('.gallery').append(frame);
            }
        }).catch((error) => {
            console.error(error);
        });
    })

    $('#speak_btn').click(function (event) {
        event.preventDefault();
        recognition.start();
        recognition.onresult = (event) => {
            const speechToText = event.results[0][0].transcript;
            console.log(speechToText);
            $('#query_txt').val(speechToText);
        }
    })

    $("#submit_btn").click(function (event) {
        event.preventDefault();
        last_index_quote = encoded.lastIndexOf('"');
        fileExt = filename.split(".").pop();
        if (fileExt == 'jpg' || fileExt == 'jpeg') {
          encoded = encoded.substring(33, last_index_quote);
        }
        else {
          encoded = encoded.substring(32, last_index_quote);
        }
        console.log(encoded)
        var customLabels = $('#custom-labels').val()
        axios.put(
            `https://zw6zd19ubb.execute-api.us-east-2.amazonaws.com/dev/b2-photo-uploads/${filename}`, 
            encoded, 
            {
                headers: {
                    'x-amz-meta-customLabels': customLabels
                },
            })
    })
}