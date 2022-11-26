
// Check for Window load
//$(window).load(function(){
//Begin Document Ready
$(document).ready(function(){
  //Menu & pages
  var linkPage = '';
  //flag to toggle between home and other pages
  var homeFlag = 0;
  
  // Call to slide out Extended view
  function pageOn(){
    $('#main-menu').addClass('main-menu-pgactive');
    $('#section-home').addClass('vcard-body-pgactive');    
    $('.profileActive').removeClass('profileActive');    
    //swithcing to profile pic 1
    $('#profile-pic2').addClass('profileActive');
    
    homeFlag = 1;
  }

  //call to slide in extended view
  function pageOff(){
    $('.section-page-active').removeClass('section-page-active');
    $('#main-menu').removeClass('main-menu-pgactive');
    $('#section-home').removeClass('vcard-body-pgactive');
    $('.profileActive').removeClass('profileActive');
    // switching to profile pic1
    $('#profile-pic1').addClass('profileActive');
    homeFlag = 0;
  }
  // activate the element /page selected
$(".link-page").on('click', function(event){
  event.preventDefault();
  $('.menuActive').removeClass('menuActive');  
  $(this).addClass('menuActive');
  linkPage = $(this).attr('href');
  $('.section-page-active').removeClass('section-page-active');
  $(linkPage).addClass('section-page-active');
  pageOn();
});

  // Toggle page screens based on Home flag
  $(".link-home").on('click', function(event){
  event.preventDefault();
  // Home is not active
    if (homeFlag == 1) {
    $('.menuActive').removeClass('menuActive');
    $(this).addClass('menuActive');
    pageOff();
  }  
  });
  
});
  //end of document ready
  
// });
//End of window load