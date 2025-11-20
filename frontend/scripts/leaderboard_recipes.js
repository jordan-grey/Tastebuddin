const API_BASE = "http://localhost:5001";
// const FEED_ENDPOINT = "/feed/sarah_test";
/*
This is an example of what will be sent as a Author leaderboard
leaderboard = [
                {
                    "rank": idx + 1,
                    "author": r["authorname"],
                    "title": r["title"],
                    "likes": r.get("likes", 0),
                    "datecreated": r.get("datecreated")
                }
                for idx, r in enumerate(response.data)
            ]
                */
let fakeLeaderboard = [
                {
                    "rank": 1,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 2,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 3,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 4,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 5,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 6,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 7,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 8,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },
                {
                    "rank": 9,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },{
                    "rank": 10,
                    "author": "STINKYBOi",
                    "title": "BEST foOED EAT ME",
                    "likes": 98010000000,
                    "datecreated": '2025-11-18T14:30:00.123456'
                },

            
            ];


let dragging = false;

function fillLeaderboard() {
    for (let i = 1; i <= 10; i++) {//row being each row that is passed in
        const r = fakeLeaderboard[i-1];//Currently fake for testing purposes
        let username = document.querySelector("#username"+ i);
        let total_likes = document.querySelector("#total_likes"+ i);
        let title = document.querySelector("#title"+ i);
        
        if (r.rank == i){
            username.innerHTML = r.author
            total_likes.innerHTML = r.likes
            title.innerHTML = r.title
        }
        else {
            console.error("Something in leaderboard went wrong," +
                i + " is not the same as " + r.rank);
        }
            
    }
}
fillLeaderboard();