function (doc) {
    if (doc.sentiment < 0) { 
      emit([doc.sentiment,doc.place.bounding_box.coordinates], 1);
    }
}
