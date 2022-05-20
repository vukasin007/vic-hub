function filterCategories() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("searchCategory");
    filter = input.value.toUpperCase();
    div = document.getElementById("categoriesDiv");
    aa = div.getElementsByTagName("a");
    for (i = 0; i < aa.length; i++) {
        txtValue = aa[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            aa[i].style.display = "";
        } else {
            aa[i].style.display = "none";
        }
    }
}

function addCategory() {
    var button, input, submit;
    input = document.getElementById("inputAddCategory");
    button = document.getElementById("buttonAddCategory");
    submit = document.getElementById("submitAddCategory");

    button.style.display = "none";
    input.style.display = "";
    submit.style.display = "";

}