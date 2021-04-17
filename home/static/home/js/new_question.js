function disableAllSubSubject() {
    for (let i = 0; i < ID_Sub_Subject.length; i++) {
        if (i !== 0) {
            ID_Sub_Subject[i].style.display = 'none';
        }
    }
}

function showBibleSubSubjectsAndBooks() {
    ID_Sub_Subject[1].style.display = "";
    ID_Sub_Subject[2].style.display = "";
    ID_Sub_Subject[3].style.display = "";
    ID_Book[2].style.display = "";
    ID_Book[3].style.display = "";
    ID_Book[4].style.display = "";
}

function showBiologySubSubjectsAndBooks() {
    ID_Sub_Subject[4].style.display = "";
    ID_Sub_Subject[5].style.display = "";
    ID_Sub_Subject[6].style.display = "";
    ID_Book[1].style.display = "";
}

function showChemistrySubSubjectsAndBooks() {
    ID_Sub_Subject[7].style.display = "";
    ID_Sub_Subject[9].style.display = "";
}

function showEnglishSubSubjectsAndBooks() {
    ID_Sub_Subject[11].style.display = "";
    ID_Sub_Subject[12].style.display = "";
}

function showGeographySubSubjectsAndBooks() {
    ID_Sub_Subject[13].style.display = "";
    ID_Sub_Subject[14].style.display = "";
}

function showLitratureSubSubjectsAndBooks() {
    ID_Book[5].style.display = "";
    ID_Book[7].style.display = "";

}

function showHistorySubSubjectsAndBooks() {
    ID_Sub_Subject[16].style.display = "";
    ID_Sub_Subject[17].style.display = "";
    ID_Sub_Subject[18].style.display = "";
    ID_Sub_Subject[28].style.display = "";
    ID_Sub_Subject[29].style.display = "";
    ID_Book[6].style.display = "";
    ID_Book[8].style.display = "";

}

function showHebrewSubSubjectsAndBooks() {
    ID_Sub_Subject[19].style.display = "";
    ID_Sub_Subject[20].style.display = "";
    ID_Sub_Subject[21].style.display = "";
    ID_Book[9].style.display = "";
}

function showMathSubSubjectsAndBooks() {
    ID_Sub_Subject[22].style.display = "";
    ID_Sub_Subject[23].style.display = "";
    ID_Sub_Subject[24].style.display = "";
    ID_Book[10].style.display = "";
}

function showPhysicsSubSubjectsAndBooks() {
    ID_Sub_Subject[8].style.display = "";
    ID_Sub_Subject[10].style.display = "";
    ID_Sub_Subject[15].style.display = "";
    ID_Sub_Subject[25].style.display = "";
    ID_Sub_Subject[26].style.display = "";
    ID_Sub_Subject[27].style.display = "";
    ID_Book[11].style.display = "";
}


function disableAllBooks() {
    for (let i = 0; i < ID_Book.length; i++) {
        if (i !== 0) {
            ID_Book[i].style.display = 'none';
        }
    }
}

let ID_Title = document.querySelector('#id_title');
let ID_Subject = document.querySelector('#id_subject');
let ID_Sub_Subject = document.querySelector('#id_sub_subject');
let ID_Grade = document.querySelector('#id_grade');
let ID_Book = document.querySelector('#id_book');
let ID_Book_Page = document.querySelector('#id_book_page');
let ID_Content = document.querySelector('#id_content');

disableAllSubSubject();
disableAllBooks();
ID_Book_Page.disabled = true;
ID_Book_Page.min = 1;

ID_Book.onchange = function () {
    if (ID_Book.value == "") {
        ID_Book_Page.disabled = true;
    }
    else {
        ID_Book_Page.disabled = false;
    }
}

ID_Subject.onchange = function () {
    switch (ID_Subject.value) {
        case "1":   //  user chose "Bible"
            disableAllBooks();
            disableAllSubSubject();
            showBibleSubSubjectsAndBooks();
            break;
        case "2":   //  user chose "Biology"
            disableAllBooks();
            disableAllSubSubject();
            showBiologySubSubjectsAndBooks();
            break;
        case "3":   //  user chose "Chemistry"
            disableAllBooks();
            disableAllSubSubject();
            showChemistrySubSubjectsAndBooks();
            break;
        case "4":   //  user chose "English"
            disableAllBooks();
            disableAllSubSubject();
            showEnglishSubSubjectsAndBooks();
            break;
        case "5":   //  user chose "Geography"
            disableAllBooks();
            disableAllSubSubject();
            showGeographySubSubjectsAndBooks();
            break;
        case "6":   //  user chose "Litrature"
            disableAllBooks();
            disableAllSubSubject();
            showLitratureSubSubjectsAndBooks();
            break;
        case "7":   //  user chose "History"
            disableAllBooks();
            disableAllSubSubject();
            showHistorySubSubjectsAndBooks();
            break;
        case "8":   //  user chose "Hebrew"
            disableAllBooks();
            disableAllSubSubject();
            showHebrewSubSubjectsAndBooks();
            break;
        case "9":   //  user chose "Math"
            disableAllBooks();
            disableAllSubSubject();
            showMathSubSubjectsAndBooks();
            break;
        case "10":  //  user chose "Physics"
            disableAllBooks();
            disableAllSubSubject();
            showPhysicsSubSubjectsAndBooks();
            break;
        default:    //  user chose "----"
            disableAllSubSubject();
            disableAllBooks();
    }
}
