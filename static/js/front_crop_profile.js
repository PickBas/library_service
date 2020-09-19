let avatar_input = document.getElementById('id_base_image')
const avatar = document.getElementById('avatar')

function changeImage (e) {
    var reader = new FileReader()

    reader.onload = function (e) {
        avatar.src = e.target.result

        cropper.destroy()

        cropper = new Cropper(avatar, {
            checkCrossOrigin: false,
            viewMode: 1,
            aspectRatio: 1/1,
            minCropBoxWidth: 256,
            minCropBoxHeight: 256,
        })
    }

    reader.readAsDataURL(avatar_input.files[0])
}

let cropper = new Cropper(avatar, {
    checkCrossOrigin: false,
    viewMode: 1,
    aspectRatio: 1/1,
    minCropBoxWidth: 256,
    minCropBoxHeight: 256,
})

function setDataAndSubmit () {
    let form = document.getElementById('avatars_form')

    let cropData = avatar.cropper.getData()
    document.getElementById('id_x').value = cropData["x"]
    document.getElementById('id_y').value = cropData["y"]
    document.getElementById('id_height').value = cropData["height"]
    document.getElementById('id_width').value = cropData["width"]
    form.submit()
}

avatar_input.addEventListener("change", changeImage);