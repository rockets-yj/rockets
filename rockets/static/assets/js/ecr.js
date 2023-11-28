function createECR() {
    $.ajax({
        url: '/create_ecr/',
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            alert('ECR created successfully!');
        },
        error: function(error) {
            alert('Error creating ECR: ' + error.responseJSON.message);
        }
    });
}
