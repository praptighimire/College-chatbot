function openModal() {
  document.getElementById('loginModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('loginModal').style.display = 'none';
}

// Optional: Close modal when clicked outside
window.onclick = function(event) {
  const modal = document.getElementById('loginModal');
  if (event.target === modal) {
    modal.style.display = "none";
  }
};

// Optionally, you can add more logic for student/guest/member here
// For example, redirect or show a message if needed