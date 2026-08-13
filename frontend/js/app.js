// Simple client-side demo logic: auth and complaint storage in localStorage
(function(){
  const authLink = document.getElementById('auth-link');
  function currentUser(){
    return JSON.parse(localStorage.getItem('user')||'null');
  }

  function updateAuthLinks(){
    if(!authLink) return;
    const u = currentUser();
    authLink.textContent = u? 'Logout' : 'Login';
    authLink.href = u? '#' : 'login.html';
  }

  // populate complaint list on index
  function renderIndexComplaints(){
    const el = document.getElementById('complaint-list');
    if(!el) return;
    const u = currentUser();
    const all = JSON.parse(localStorage.getItem('complaints')||'[]');
    const mine = u? all.filter(c=>c.userEmail===u.email) : [];
    if(!u) { el.innerHTML = 'Please log in to see complaints.'; return }
    if(mine.length===0) el.innerHTML = '<div class="muted">No complaints yet.</div>'
    else el.innerHTML = mine.map(c=>`<div class="card"><strong>${c.title}</strong><div class="muted">ID: ${c.id} • Status: ${c.status}</div></div>`).join('')
  }

  // profile
  function renderProfile(){
    const u = currentUser();
    if(!u) return;
    const name = document.getElementById('user-name');
    const email = document.getElementById('user-email');
    const list = document.getElementById('user-complaints');
    if(name) name.textContent = u.name||'Citizen'
    if(email) email.textContent = u.email
    const all = JSON.parse(localStorage.getItem('complaints')||'[]');
    const mine = all.filter(c=>c.userEmail===u.email)
    if(list) list.innerHTML = mine.length? mine.map(c=>`<div class="card"><strong>${c.title}</strong><div class="muted">ID: ${c.id} • Status: ${c.status}</div></div>`).join('') : '<div class="muted">No complaints</div>'
  }

  // simple signup/login handlers attach
  const signup = document.getElementById('signup-form');
  if(signup) signup.addEventListener('submit', e=>{
    e.preventDefault();
    const fd = new FormData(signup);
    const user = {name:fd.get('name'), email:fd.get('email'), password:fd.get('password')};
    localStorage.setItem('user', JSON.stringify(user));
    alert('Account created and signed in');
    updateAuthLinks();
    location.href='profile.html';
  })

  const login = document.getElementById('login-form');
  if(login) login.addEventListener('submit', e=>{
    e.preventDefault();
    const fd = new FormData(login);
    const stored = JSON.parse(localStorage.getItem('user')||'null');
    if(stored && stored.email===fd.get('email') && stored.password===fd.get('password')){
      localStorage.setItem('user', JSON.stringify(stored));
      alert('Signed in');
      updateAuthLinks();
      location.href='profile.html';
    } else {
      alert('Invalid credentials or user does not exist. Sign up first.');
    }
  })

  // logout via auth-link
  if(authLink) authLink.addEventListener('click', e=>{
    const u = currentUser();
    if(u){ localStorage.removeItem('user'); updateAuthLinks(); location.href='index.html'; }
  })

  // init renders
  updateAuthLinks();
  renderIndexComplaints();
  renderProfile();
})();
