var encoded = null;
var fileExt = null;

window.onload = function () {
    $("#upload_files").change(function(e) {
        for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {
    
            var file = e.originalEvent.srcElement.files[i];
            fileExt = file.name.split(".").pop();
    
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
            $("#upload_files").after(img);
        }
    });

    $("#submit_btn").click(function (event) {
        event.preventDefault();
        last_index_quote = encoded.lastIndexOf('"');
        if (fileExt == 'jpg' || fileExt == 'jpeg') {
          encoded = encoded.substring(33, last_index_quote);
        }
        else {
          encoded = encoded.substring(32, last_index_quote);
        }
        console.log(encoded)
        
        axios.put("https://zw6zd19ubb.execute-api.us-east-2.amazonaws.com/dev/b2-photo-uploads/test.jpeg", encoded, {
            headers :{
                'x-amz-meta-customLabels': 'Capoo',
            },
        })
    })
}