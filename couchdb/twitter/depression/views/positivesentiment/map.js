function (doc) {
    if (doc.sentiment > 0) { 
      emit([doc.place.bounding_box.coordinates], doc.sentiment);
    }
}
