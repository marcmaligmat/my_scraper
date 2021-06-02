import React from 'react';

const CommentForm = () => {
    return(
        <div className="review-comment-section">
            <div className="row">
                <div className="col-12 col-md-12 col-lg-12 col-xl-8">
                    <div className="reviews-title leave-opinion">
                        <h3>Leave Your Comment here (login required) </h3>
                    </div>
                    <form>
                        <div className="row">
                            <div className="col-12">
                                <div className="form-group">
                                    <label for="last" className="color-green">Comment</label>
                                        <textarea className="form-control col-md-12" id="exampleFormControlTextarea1" name="body" placeholder="Write your Comment here ... "></textarea>
                                </div>
                            </div>
                            <div className="col-md-12">
                                <button type="submit" className="btn btn-primary review-comment"><i className="fa fa-check" aria-hidden="true"></i> Post Comment</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
    
}
export default CommentForm;