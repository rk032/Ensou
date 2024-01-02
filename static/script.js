const box=document.querySelector(".box")
const reglink=document.querySelector(".register")
const login=document.querySelector(".login-pop")
const sub=document.querySelector(".sub")
const close=document.querySelector(".close")
const player=document.querySelector(".player")
const stuff=document.querySelector(".stuff")
const lib=document.querySelector(".lib")
const toggle=document.querySelector(".toggle")
const toggle1=document.querySelector(".toggle1")
var isPlaying = true;
var rep=false;

reglink.addEventListener('click',()=>{
    box.classList.add('active');
})
login.addEventListener('click',()=>{
    box.classList.add('active-pop');
    player.classList.add('nactive')
})
sub.addEventListener('click',()=>{
    box.classList.remove('active-pop');
    box.classList.remove('active');
})
close.addEventListener('click',()=>{
    box.classList.remove('active-pop');
    player.classList.remove('nactive');
    
})
function libr(){
        
        window.location.href = "/pl";
   
}
function rec(){
        window.location.href="/recom";
}
function plays(){
    fetch("/play")
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
function pre(){
    fetch("/prev")
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
function nex(){
    fetch("/next")
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
function pause(){
    fetch("/pau")
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
function unpause(){
    fetch("/unpau")
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
function curr(text){
    var a=text.textContent;
    fetch(`/playcurr?text=${a}`)
    .then(response => response.text())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
function rdown(text){
  var a=text.textContent;
  fetch(`/recdownload?text=${a}`)
  .then(response => response.text())
  .then(data => {
      console.log(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
function togglePlayPause() {

        let t=document.getElementById("toggle");
        let t1=document.getElementById("toggle1");
        if(isPlaying){
  
            isPlaying = !isPlaying;
            pause();
            t.style.display="none";
            t1.style.display="inline-block";
        }
        else{
         
            isPlaying = !isPlaying;
            unpause();
            t1.style.display="none";
            t.style.display="inline-block";

        }
}
function rept(){
  alert("repeat on");
  fetch("/repe")
  .then(response => response.json())
  .then(data => {
      console.log(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
function repf(){
  alert("repeat off");
  fetch("/norepe")
  .then(response => response.json())
  .then(data => {
      console.log(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
function repeater(){
      if(rep==false){
        rep=!rep;
        rept();
      }
      else{
        rep=!rep;
        repf();
      }


}
function get_l(){
  fetch("/lyric")
  .then(response => response.json())
  .then(data => {
      console.log(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}