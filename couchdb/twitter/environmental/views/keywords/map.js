function (doc) {
  var climate = ['global warming', 'climate', 'climatechange','global heating', 'emission', 'environmental', 'green', 'solar', 'carbon', 'greenhouse gas', 'coal', 'coral', 'temperature', 'sea level', 'reef', 'warmist'];
  var words = doc.text.toLowerCase().split(/\W+/);
  var words2 = doc.extended_tweet.full_text.toLowerCase().split(/\W+/);
  if ((words.filter(value => climate.includes(value))).length > 0){
      emit([doc.sentiment, doc.place.bounding_box.coordinates], 1);
  }
  else if ((words2.filter(value => climate.includes(value))).length > 0){
    emit([doc.sentiment, doc.place.bounding_box.coordinates], 1);
  }
}
