$(document).ready(function(){
    function getFunctions(slideDiv) {
        var index = 0
        var images = slideDiv.find($("img"))
        
        
        return {
            slide : function(n) {
                index += n
                if (index >= images.length) {index = 0}
                if (index < 0) {index = images.length-1}
                console.log(index)
            },
            display : function() {
                images.css( "display", "none" );
                images.eq(index).css( "display", "block" );
            }
        }
    }
    
    var slideFunctions = [];
    $(".slideshow").each(function(index) {
        var f = getFunctions($(this))
        slideFunctions.push(f)
        $(this).find(".leftButton").click(function(){
            f.slide(-1)
            f.display()
        })
        $(this).find(".rightButton").click(function(){
            f.slide(1)
            f.display()
        })
    })
    
    slideFunctions.forEach(function(item, index) {
        item.display()
        item.slide(1)
        item.slide(1)
        item.slide(1)
        item.display()
    })
})
