document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelectorAll('#like').forEach(function(button){
        button.onclick = function() {
            react_post(this,this.dataset.id, this.dataset.post);
        };
    });
  
});

function react_post(button,id, post){
    console.log(id)
    console.log(post)

    fetch(`/like/${id}`,{
        method: 'POST',
        body: JSON.stringify({
            post: post
        })
    })

    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        count = button.parentElement.querySelector('#count')
        x = Number(count.innerHTML.split(" ")[1])
        if (post === "like"){
            button.innerHTML =`<i class="bi bi-hand-thumbs-down-fill"></i>UnLike`
            button.dataset.post = "unlike"
            x++;
            count.innerHTML = `Likes: ${x}`;
        }
        else {
            button.innerHTML = `<i class="bi bi-hand-thumbs-up-fill"></i>Like`
            button.dataset.post = "like"
            x--;
            count.innerHTML = `Likes: ${x}`;
        }
        console.log(button.dataset.post)
    });
    
    return false;
}