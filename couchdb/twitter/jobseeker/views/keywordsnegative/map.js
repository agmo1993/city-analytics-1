function (doc) {
  var keywords = ['jobseeker','unemployment','centrelink','jobkeeper','welfare','dole','jobmaker','austudy','newstart'];
  var words = doc.text.toLowerCase().split(/\W+/);
  var words2 = doc.extended_tweet.full_text.toLowerCase().split(/\W+/);
  if ((words.filter(value => keywords.includes(value))).length > 0 && (doc.sentiment < 0)){
      emit([doc.place.bounding_box.coordinates], doc.sentiment);
  }
  else if ((words2.filter(value => keywords.includes(value))).length > 0 && (doc.sentiment < 0)){
    emit([doc.place.bounding_box.coordinates], doc.sentiment);
  }
}
