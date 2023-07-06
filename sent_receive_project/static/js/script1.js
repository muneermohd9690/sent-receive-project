/***  for adding to cart ***/
function getCartData(detailId, action){
  console.log(detailId)
  console.log(action)
  console.log(user)
  if (user === 'AnonymousUSer'){
    addCookieItem()
  }else {
    updateUserOrder(detailId,action)

  }
}

function addCookieItem(detailId,action){
    console.log('Not logged in')
}

function updateUserOrder(detailId,action){
    console.log('User is logged in,sending data')
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
/***  for adding to cart ***/


/***  for bulk delete ***/
/*function getBulkDeleteids(item_id){
        if(confirm("sure you want to delete?")){
            var id=[];
            $(':checkbox:checked').each(function(i)
            {
                id[i]=$(this).val()
            })
            if(id.length===0){
                alert("please select an item")
            }
            else{
                console.log(id)
                console.log(item_id)
                BulkDelete(id,item_id)
            }
        }
}

function BulkDelete(id,item_id){
    console.log('User is logged in,sending data')
    var url= '' + item_id +'/view_tonerdetails_bulk_delete'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'id':id,'item_id':item_id})
    })
    .then((response)=>{
        responseClone = response.clone();
        return response.json()
    })
    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })

}*/
/***  for bulk delete ***/