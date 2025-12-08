(function () {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.replace('login.html')
    return
  }
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    if (payload.exp < Math.floor(Date.now() / 1000)) {
      localStorage.clear()
      window.location.replace('login.html')
    } else {
      document.documentElement.style.display = 'block'
    }
  } catch (e) {
    localStorage.clear()
    window.location.replace('login.html')
  }
})()
