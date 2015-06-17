
public class User implements EventHandler {
	
	int workingCount;
	int failureCount;
	
	public User() {
		workingCount=0;
		failureCount=0;
	}

	@Override
	public void respondToEvent(Event e, Simulation s) {
		// TODO Auto-generated method stub
		if (e.getType()==s.userCheck) {
                    if (s.m.working) {
                        workingCount++;
                    } else {
                        failureCount++;
                    }
		}
		System.out.println(e.getTime()+" user check: working "+(100*workingCount)/(workingCount+failureCount)+"%");
		e.setTime(s.now+60);
		s.scheduleEvent(e);
	}

}
