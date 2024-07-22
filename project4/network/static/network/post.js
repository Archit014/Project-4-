document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelectorAll('#edit').forEach(function(button){
        button.onclick = function() {
            edit_post(this,this.dataset.identity);
        };
    });
});

function edit_post(edit,id) {

    console.log(edit)
    edit.parentElement.querySelector('#content').innerHTML=`<textarea class="form-control" id="compose-body" placeholder="Body" name="content"></textarea>`

    const button = document.createElement('button')
    button.innerHTML = `Save`;
    button.className = "btn btn-primary"
    edit.parentElement.querySelector('#compose-body').value = '';

    const NewBody = edit.parentElement.querySelector('#compose-body')

    button.addEventListener('click', function() {
        const content = NewBody.value;

        fetch(`/post/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            content:content
            })
        })
        .then(response => response.json())
        .then(result => {
          // Print result
          console.log(result);
          edit.parentElement.querySelector('#content').innerHTML=`${content}`
        });
    
        return false;
    });

    edit.parentElement.querySelector('#content').append(button);

}
