
function getCartData(detailId, action){
  console.log(detailId)
  console.log(action)
  console.log(user)
  if (user === 'AnonymousUSer'){
    console.log('Not Logged in')
  }else {
    updateUserOrder(detailId,action)
  }
}

function updateUserOrder(detailId,action){
    console.log('User is loged in,sending data')

    var url='/sent_items/update_items/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'detailId':detailId,'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}
