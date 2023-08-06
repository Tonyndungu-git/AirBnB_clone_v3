$(document).ready(function() {
  // Function to update the availability status based on API response
  function updateApiStatus() {
    $.get('http://0.0.0.0:5001/api/v1/status/', function(data) {
      if (data.status === 'OK') {
        $('#api_status').addClass('available');
      } else {
        $('#api_status').removeClass('available');
      }
    });
  }

  // Call the updateApiStatus function on page load
  updateApiStatus();
});
