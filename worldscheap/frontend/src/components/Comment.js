import React, { useState } from 'react'

const Comment = (props) =>{
    // console.log(props.comments)
    return(
        <div>
            {props.comments.map((comment) => (
                <div className="row">
                    <div className="col-12 col-md-8">
                        <div className="row">
                            <div className="col-12">
                                <div className="media">
                                    <div className="media-left media-middle">
                                    <a href="#">
                                        <img className="user_image" src="https://scontent-hkt1-2.xx.fbcdn.net/v/t1.0-1/p200x200/131339282_10218796574449408_3453495510447217191_n.jpg?_nc_cat=102&ccb=2&_nc_sid=7206a8&_nc_eui2=AeFl7tpU5DPj_J-RdJzc_tQRoRwP-zQfx5qhHA_7NB_HmjyVBLk8zsZFLHiXEuomOMI&_nc_ohc=c4DTPdBcLOwAX80slBq&_nc_ht=scontent-hkt1-2.xx&tp=6&oh=e03c6b8c5b9750f800aec401a9019487&oe=6002A30E" alt="client-img"  />
                                    </a>
                                    </div>
                                    <div className="media-body">
                                        <h4 className="media-heading client-title color-gray">
                                        {comment.author}
                                            <span class="review-date pull-right ">November 17, 2016</span>
                                        </h4>
                                        <span className="badge badge-primary">Moderator</span>
                                        <p>{comment.body}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {/* <div className="col-12 col-md-6 review-date-time">
                        <p className="review-date">November 17, 2016</p>
                        <p className="review-time">at 11:52 pm</p>
                    </div> */}
                </div>
            ))}
        </div>
    );
}

export default Comment;