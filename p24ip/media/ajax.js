function getXmlHttp()
{
  var xmlHttp;
  try
  {
    xmlHttp = new XMLHttpRequest(); 
  } 
  catch(e) 
  {
    try
    {
      xmlHttp = new ActiveXObject("Msxml2.XMLHTTP"); 
    } 
    catch(e) 
    {
      try 
      {
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP"); 
      } 
      catch(e) 
      {
        alert("Twoja przeglądarka nie obsługuje AJAX!");
        return false;
      }
    }
  }
  return xmlHttp; 
}