
public class Event {

	private double time;
	private int type;
	private EventHandler handler;
	
	
	public Event() {
		time = 0;
		type = 0;
	}
	
	public void setTime(double eventTime) {
		time = eventTime;
	}
	
	public void setType(int eventType) {
		type = eventType;
	}

	public double getTime() {
		return time;
	}
	
	public int getType() {
		return type;
	}
	
	public EventHandler getHandler() {
		return handler;
	}
	
	public void setHandler(EventHandler newHandler) {
		handler = newHandler;
	}
	
	public String toString() {
		return "time="+time+":type="+type;
	}
	
}
