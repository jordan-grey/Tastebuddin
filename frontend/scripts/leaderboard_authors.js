const API_BASE = "http://localhost:5001";
// const FEED_ENDPOINT = "/feed/sarah_test";
/*
This is an example of what will be sent as a Author leaderboard
leaderboard = [
                {"rank": idx + 1, "author": author, "total_likes": likes}
                for idx, (author, likes) in enumerate(ranked)
            ]
                */
let fakeLeaderboard = [
        {
            "rank": 1,
            "author": "Timmy",
            "total_likes": 798
        },
        {
            "rank": 2,
            "author": "Henry",
            "total_likes": 696
        },
        {
            "rank": 3,
            "author": "Chad",
            "total_likes": 666
        },
        {
            "rank": 4,
            "author": "Samuel",
            "total_likes": 643
        },
        {
            "rank": 5,
            "author": "Satan",
            "total_likes": 534
        },
        {
            "rank": 6,
            "author": "Scott",
            "total_likes": 322
        },
        {
            "rank": 7,
            "author": "Token_girl_name",
            "total_likes": 231
        },
        {
            "rank": 8,
            "author": "Sebastian",
            "total_likes": 100
        },
        {
            "rank": 9,
            "author": "Peter",
            "total_likes": 97
        },
        {
            "rank": 10,
            "author": "Logan",
            "total_likes": 34
        }
            
];


let dragging = false;

function fillLeaderboard() {
    for (let i = 1; i <= 10; i++) {//row being each row that is passed in
        const r = fakeLeaderboard[i-1];//Currently fake for testing purposes
        let username = document.querySelector("#username"+ i);
        let total_likes = document.querySelector("#total_likes"+ i);
        
        if (r.rank == i){
            username.innerHTML = r.author
            total_likes.innerHTML = r.total_likes
        }
        else {
            console.error("Something in leaderboard went wrong," +
                i + " is not the same as " + r.rank);
        }
            
    }
}
fillLeaderboard();