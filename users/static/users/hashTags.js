const ul = document.getElementById("hashTags"),
input = document.getElementById("hashTags"),
tagNumb = document.querySelector(".details span");
let maxTags = 10,
tags = [];
countTags();
createTag();
function countTags(){
    input.focus();
    tagNumb.innerText = maxTags - tags.length;
}
function createTag(){
    console.log("CALLED!")
    ul.querySelectorAll("li").forEach(li => li.remove());
    tags.slice().reverse().forEach(tag =>{
        let liTag = `<li>${tag} <i class="uit uit-multiply" onclick="remove(this, '${tag}')"></i></li>`;
        ul.insertAdjacentHTML("afterbegin", liTag);
    });
    countTags();
    document.getElementById('suggestions').innerHTML = "";
}
function remove(element, tag){
    let index  = tags.indexOf(tag);
    tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
    element.parentElement.remove();
    countTags();
}
function addTag(e){
    if(e.key == "Enter"){
        console.log(e);
        console.log(e.target)
        console.log(e.target.value)
        let tag = e.target.value.replace(/\s+/g, ' ');
        if(tag.length > 1 && !tags.includes(tag)){
            if(tags.length < 10){
                tag.split(',').forEach(tag => {
                    console.log(tag)
                    tags.push(tag);
                    createTag();
                });
            }
        }
        e.target.value = "";
    }
}
input.addEventListener("keypress", addTag);
const removeBtn = document.querySelector(".details button");
removeBtn.addEventListener("click", () =>{
    tags.length = 0;
    ul.querySelectorAll("li").forEach(li => li.remove());
    countTags();
});





(function () {
  "use strict";
  let inputField = document.getElementById('userInputTags');
  let ulField = document.getElementById('suggestions');

  let newElement = document.createElement("p");

  // Adding some styles here
  newElement.style.fontSize = "20px";
  newElement.style.paddingTop = "15px";
  ulField.style.border = "none";



  const question = document.createTextNode("Do You Mean ? ");
  newElement.appendChild(question);

  inputField.addEventListener('input', changeAutoComplete);
  ulField.addEventListener('click', selectItem);

  function changeAutoComplete({ target }) {
    let data = target.value;
    ulField.innerHTML = ``;
    if (data.length) {
      let autoCompleteValues = autoComplete(data);
      autoCompleteValues.forEach(value => { addItem(value); });
      ulField.insertBefore(newElement, ulField.firstChild);
    }
  }

  function autoComplete(inputValue) {
    let destination = ["Italy", "Spain", "Portugal", "Brazil"];
    return destination.filter(
      (value) => value.toLowerCase().includes(inputValue.toLowerCase())
    );
  }

  function addItem(value) {
    ulField.innerHTML = ulField.innerHTML +`<li>${value}</li>`;
  }

  function selectItem({ target }) {
    if (target.tagName === 'LI') {
      // inputField.value = target.textContent;
      ulField.innerHTML = ``;
      tags.push(target.textContent);
      createTag();
      inputField.value = "";

    }
  }

})();