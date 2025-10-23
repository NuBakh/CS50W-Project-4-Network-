// Select all post elements
let posts= document.querySelectorAll(".posts")
let userUsername=document.querySelector("#user-username").textContent

// Iterate over each post
posts.forEach(post=>{
  let userPost=post.querySelector(".userpost").textContent
  let editBtn= post.querySelector(".edit")
  let deleteBtn = post.querySelector(".delete")
  let like=post.querySelector(".like")
  let likeCount=post.querySelector(".like-count")

  // Get CSRF token from the page
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Get the post ID from data attribute
  let postId=post.dataset.postId

  
  // Like/Unlike functionality
  like.onclick=function(){
 
    fetch(`/like/${postId}/`, {
      method: 'POST',
      headers: {
         "Content-Type": "application/json",
         "X-CSRFToken": csrftoken},
      body: JSON.stringify({
        "post_id":postId,
        "likeCount": likeCount})
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        like.textContent = result.liked ? "Unlike" : "Like";
        likeCount.textContent = result.like_count;});

  }


  
  // Delete post functionality
  deleteBtn.onclick= function(){
      
    fetch(`/delete/${postId}/`, {
        method: 'DELETE',
        headers: {
          "X-CSRFToken": csrftoken,} 
      })
    .then(response => response.json())
    .then(result => {
          if(result.success){

            post.style.transition = "opacity 0.4s ease";
            post.offsetHeight; 
            post.style.opacity = 0;

            setTimeout(() => post.remove(), 400);}
      });
  }

  // Edit post functionality
  editBtn.onclick=function(){
    // Prevent creating multiple textareas
    if (post.querySelector(".postarea")) {return;}

    let a=post.querySelector(".post-content")
    a.style.display="none";

    // Create textarea for editing
    let content=document.createElement("textarea")
    content.classList.add("postarea")
            
    // Create save button
    let save=document.createElement("button")
    save.innerHTML="Save"
    save.className="save btn btn-primary"

    let postone = this.closest(".posts");

    let divContainer=document.createElement("div")
    divContainer.className="divContainer"

    divContainer.appendChild(content)
    divContainer.appendChild(save)
    postone.appendChild(divContainer)
        
    let saveButton=post.querySelector(".save")
    content.value=a.textContent




    // Save edited post
    saveButton.onclick = function() {

      let newContent = content.value; 
        
      fetch(`/edit/${postId}/`, {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken},
          body: JSON.stringify({
            "post_id":postId,
            "content": newContent,})
        })
      .then(response => response.json())
      .then(result => {
            // Print result
            console.log(result);
            a.textContent = result.content;
            a.style.display = "block";
            content.remove()
            saveButton.remove()});   
    };
      
  }


})







 

