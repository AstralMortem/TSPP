const modal = document.getElementById("delete-modal")
function closeModal(){
    modal.remove()
}

const full_name_field = document.getElementById("div_id_full_name")
const organisation_name = document.getElementById("div_id_organization_name")
let volunter_box = document.getElementById('id_is_organisation')

if(volunter_box.checked){
    full_name_field.classList.add("is-hidden")
    organisation_name.classList.remove("is-hidden")
    
}else{
    full_name_field.classList.remove("is-hidden")
    organisation_name.classList.add("is-hidden")
}

volunter_box.addEventListener("change",function(e){
    let val = e.target.checked
    if(val){
        full_name_field.classList.add("is-hidden")
        organisation_name.classList.remove("is-hidden")
    }else{
        full_name_field.classList.remove("is-hidden")
        organisation_name.classList.add("is-hidden")
    }
})



