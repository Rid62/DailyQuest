const password = document.getElementById('password');
const confirm = document.getElementById('confirm_password');

confirm.addEventListener('input', () => {
    if (password.value !== confirm.value) {
        confirm.style.borderColor = 'red'; // إظهار إطار أحمر عند الخطأ
    } else {
        confirm.style.borderColor = 'green'; // إطار أخضر عند التطابق
    }
});