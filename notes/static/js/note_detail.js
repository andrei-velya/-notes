function loadComments(){
       let baseUrl = 'http://localhost:8000';
       let noteId = $('.comments-section-ajax').data('note-id')
       let url = baseUrl + `/api/notes/${noteId}/comments`
   
       $.ajax({
               type : 'GET',
               url : url,
               success : function(response){
                                            let comments = ''
                                            $.each(
                                                   response.comments,
                                                   function(index, comment){
                                                                             comments += '<div class="comment">'
                                                                             comments += '<p class="comment-author">' + comment.profile +  '</p>'
                                                                             comments += '<p class="comment-date">' + comment.created_date + '</p>'
                                                                             comments += '<p class="comment-text">' + comment.text + '</p>'
                                                                             comments += '</div>'
                                                                             }
                                                   )
                                            $('.comments-section-ajax').html(comments)
                                            }
               })
                           }

$(document).ready(
       noteId = $('.comments-section-ajax').data('note-id'),
       url = `/api/notes/${noteId}/comments`,
       console.log("Вот значение noteId:", $('.comments-section-ajax').data('note-id')),
       console.log("Вот значение noteId:", `/api/notes/${noteId}/comments`),

       loadComments() 

       )