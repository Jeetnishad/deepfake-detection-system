document.getElementById("video").onchange = function(event){

let file = event.target.files[0]

let video = document.getElementById("preview")

video.src = URL.createObjectURL(file)

}

function detect(){

let fileInput = document.getElementById("video")

let file = fileInput.files[0]

if(!file){

alert("Please select a video first")

return

}

document.getElementById("loader").style.display="block"

let formData = new FormData()

formData.append("video",file)

fetch("http://127.0.0.1:5000/detect",{

method:"POST",

body:formData

})

.then(response => response.json())

.then(data=>{

document.getElementById("loader").style.display="none"

document.getElementById("result").innerHTML="Result: "+data.result

})

}
