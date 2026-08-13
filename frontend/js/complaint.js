// complaint form handling: saves complaint + images (Base64) to localStorage
(function(){
  const form = document.getElementById('complaint-form');
  const input = document.getElementById('evidence');
  const preview = document.getElementById('preview');

  function toBase64(file){
    return new Promise((res,rej)=>{
      const r = new FileReader(); r.onload=()=>res(r.result); r.onerror=rej; r.readAsDataURL(file);
    })
  }

  if(input){
    input.addEventListener('change', async ()=>{
      preview.innerHTML='';
      for(const f of input.files){
        const src = await toBase64(f);
        const img = document.createElement('img'); img.src = src; preview.appendChild(img);
      }
    })
  }

  if(form) form.addEventListener('submit', async e=>{
    e.preventDefault();

    const fd = new FormData(form);

    const user = JSON.parse(localStorage.getItem('user') || 'null');

    if(!user){
        alert('Please login/signup before submitting a complaint.');
        return;
    }

    // Get complaint description
    const complaintText = fd.get('description');

    if(!complaintText || !complaintText.trim()){
        alert('Please enter your complaint description.');
        return;
    }

    // ================================
    // SEND COMPLAINT TO AQUASHIELD AI
    // ================================
    let aiResult = null;

    try {
        const response = await fetch('https://aquashield-ai-hxpv.onrender.com/predict',  {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                complaint: complaintText
            })
        });

        if(!response.ok){
            throw new Error('AI API request failed');
        }

        aiResult = await response.json();

        console.log('AquaShield AI Result:', aiResult);

    } catch(error) {
        console.error('AI Error:', error);

        alert(
            'Complaint could not be analyzed by AquaShield AI. ' +
            'Please make sure the AI service is running.'
        );

        return;
    }

    // ================================
    // SAVE COMPLAINT
    // ================================

    const images = [];

    for(const f of (input.files || [])){
        images.push(await toBase64(f));
    }

    const complaints = JSON.parse(
        localStorage.getItem('complaints') || '[]'
    );

    const id = 'C' +
        Date.now().toString(36).toUpperCase().slice(-8);

    const payload = {
        id: id,
        userEmail: user.email,
        title: fd.get('title'),
        description: complaintText,
        location: fd.get('location'),
        images: images,

        // ================================
        // AQUASHIELD AI ANALYSIS
        // ================================
        aiAnalysis: {
            category: aiResult.category,
            department: aiResult.department,
            priority: aiResult.priority,
            severity: aiResult.severity
        }
    };

    complaints.unshift(payload);

    localStorage.setItem(
        'complaints',
        JSON.stringify(complaints)
    );

    // Show AI result
    alert(
        'Complaint submitted successfully!\\n\\n' +
        'Category: ' + aiResult.category + '\\n' +
        'Department: ' + aiResult.department + '\\n' +
        'Priority: ' + aiResult.priority + '\\n' +
        'Severity: ' + aiResult.severity + '\\n\\n' +
        'Complaint ID: ' + id
    );

    location.href = `http://localhost:8501/?category=${encodeURIComponent(aiResult.category)}&title=${encodeURIComponent(aiResult.category)}`;
});

  // complaint tracking by ID (optional small UI)
  const track = document.getElementById('track-result');
  if(track){
    track.innerHTML = '<div class="muted">Open your profile to view complaint IDs.</div>'
  }
})();
