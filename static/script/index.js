


async function checkarts() {

    var s = document.getElementById("articoli_list");
    s.innerHTML = ""
    try {
        const res = await fetch("./get_articles?n=3");
        if(!res.ok) {
            var h = s.classList;
            h.remove("row-cols-lg-3")
            s.innerHTML = "<div class=\"d-flex justify-content-center mt-3\"><p class=\"text-center text-muted\">Non ci sono attualmente articoli!🦗</p></div>"
            return;
        }
        
        const json = await res.json();


        json.message.forEach(info => {
            console.log(info)
            var title = info.title;
            var date  = info.date;
            var img   = info.post_img;
            var id    = info.post_id;
            
            var d = new Date(date*1000);
            const day = String(d.getDate()).padStart(2, "0");
            const month = String(d.getMonth() + 1).padStart(2, "0"); // mesi 0-11
            const year = d.getFullYear();

            const date_final = `${day}/${month}/${year}`;
            s.innerHTML += "<div class=\"col\"><div class=\"card card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg\" style=\"background-image: url(./static/img/"+img+");\"><div class=\"d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1\"><h3 class=\"pt-5 mt-5 mb-4 display-6 lh-1 fw-bold\">"+title+"</h3><ul class=\"d-flex list-unstyled mt-auto\"><li class=\"me-auto\"><button type=\"button\" onclick=\"window.location = '/post?n="+id+"'\"class=\"btn btn-primary\">Vai</button></li><li class=\"d-flex align-items-center\"><i class=\"bi bi-calendar-fill me-1\"></i><small>"+date_final+"</small></li></ul></div></div>"
        });
    } catch (error) {
        console.error(error.message);
    }
}

