function (doc) {
  var words = doc.text.toLowerCase().split(/\W+/);
  var words2 = doc.extended_tweet.full_text.toLowerCase().split(/\W+/);
  if (words.includes("jobseeker")|| words.includes("unemployment") || words.includes("centrelink")){
    if (doc.sentiment < 0) { 
      emit([doc.place.bounding_box.coordinates], 1);
    }
  }
  else if (words2.includes("jobseeker")|| words2.includes("#unemployment") || words2.includes("centrelink")){
    if (doc.sentiment < 0) { 
    emit([doc.place.bounding_box.coordinates], 1);
    }
  }
  
}
