// $(document).ready(function () {
//         $('#form2').on('submit', function (event) {
//         // $('#submit').on('click', function (event) {
//             event.preventDefault();
//             console.log('newest here')
//             console.log( $('#studentID').val() )
//             console.log( $('#submit').val() )
//             $.ajax({
//                     data: {
//                         submitBtn: $('#submit').val(),
//                         student: $('#studentID').val()
//                     },
//                     type: 'POST',
//                     url: '/register'
//                 })
//                 .done(function (data) {
                    
//                     if(data.error){
//                         $('#errorAlert').text(data.error).show();
//                         $('#successAlert').hide();
//                     }
//                     else{
//                         $('#successAlert').text(data.response).show();
//                         $('#errorAlert').hide();
//                     }
//                 });
//                 // event.preventDefault();
//         });
       
//     })