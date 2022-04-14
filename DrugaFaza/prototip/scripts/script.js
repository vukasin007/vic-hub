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