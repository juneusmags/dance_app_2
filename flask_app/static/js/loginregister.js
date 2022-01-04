const modalcontainer = document.getElementById("modal-container")
const signin = document.getElementById("sign-in")
const signup = document.getElementById("sign-up")

signup.addEventListener('click', (e)=>{
    e.preventDefault()
    modalcontainer.classList.add('show')
})

signin.addEventListener('click', (e)=>{
    e.preventDefault()
    modalcontainer.classList.remove('show')
})