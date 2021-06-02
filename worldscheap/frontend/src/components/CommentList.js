import React from 'react';
import Comment from './Comment';
import axios from 'axios';


class CommentList extends React.Component{
    
    state = {
        comments:[]
    }
    
    componentDidMount() {
        const game_id = document.getElementById("gameID").textContent;
        axios.get(`http://127.0.0.1:8000/api/gamecomments/?game=${game_id}`)
            .then(res =>{
                this.setState({
                    comments: res.data    
                });
            })
    }

    render(){
        
        return(
            <Comment comments={this.state.comments}/>
        )
    }

}

export default CommentList;