(function() {
  const token = localStorage.getItem('token')
  if (!token) {
    document.documentElement.style.display = 'none'
    window.location.replace('index.html')
    return
  }
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    if (payload.exp < Math.floor(Date.now() / 1000)) {
      localStorage.clear()
      document.documentElement.style.display = 'none'
      window.location.replace('index.html')
    }
  } catch (e) {
    localStorage.clear()
    document.documentElement.style.display = 'none'
    window.location.replace('index.html')
  } finally {
    document.documentElement.style.display = 'block'
  }
})()
