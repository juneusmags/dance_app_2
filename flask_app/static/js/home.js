const timeEl = document.querySelector('.time')
const dateEl = document.querySelector('.date')




const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct","Nov", "Dec",]
    const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

function setTime(){
    const time = new Date();
    const month = time.getMonth()
    const day = time.getDay()
    const date = time.getDate()
    const hours = time.getHours()
    const hoursFroClock = hours % 12
    const minutes = time.getMinutes()
    const ampm = hours >= 12 ? 'PM' : 'AM'

    timeEl.innerHTML = `${hoursFroClock}:${minutes < 10 ? `0${minutes}`:minutes} ${ampm}`
    dateEl.innerHTML = `${days[day]} ${months[month]} ${date}`
}


setTime();



