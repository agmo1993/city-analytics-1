function (doc) {
  var words = doc.text.toLowerCase().split(/\W+/);
  var words2 = doc.extended_tweet.full_text.toLowerCase().split(/\W+/);
  if (words.includes("thelastdance")){
      emit([doc.place.bounding_box.coordinates], 1);
  }
  else if (words2.includes("thelastdance")){
    emit([doc.place.bounding_box.coordinates], 1);
  }
}
