$(document).ready(function(){
    // add slide show functionality
    // this works by finding all containers called '.slideshow' and gathering
    // all the children images into the slide show. The buttons in this
    // container called '.leftButton' and '.rightButton' shift the slide show
    // left or right accordingly
    function getFunctions(slideDiv) {
        var index = 0
        var images = slideDiv.find("img")
        
        
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
    
    // finally hide/unhide the appropriate images
    slideFunctions.forEach(function(item, index) {
        item.display()
    })
    
    
    
    
    // add the ability to hide line numbers in code segments
    $(".hide-lines-button").each(function(index) {
        var linesOn = true
        this.onclick = function(){
            if(linesOn) {
                $(this).parent().find(".lineno").css( "display", "none" );
                linesOn = false
            } else {
                $(this).parent().find(".lineno").css( "display", "inline" );
                linesOn = true
            }
        }
    })
})
