
public class Repairman implements EventHandler {

	double MTTR;
	double MTTRvariance;
	
	public Repairman() {
		MTTR = 10.0;
		MTTRvariance = 2.0;
	}
	
	
	@Override
	public void respondToEvent(Event e, Simulation s) {
		if (e.getType()==s.startRepair) {
                    System.out.println(e.getTime()+" starting repair");
                    double timeToRepair =0;

                    if(s.simulation_type==1){
                        timeToRepair = Math.abs(s.generator.nextGaussian()*MTTRvariance+MTTR);
                        e.setTime(s.now+timeToRepair);
                    } else{
                        timeToRepair = s.getNextTimeTrace();
                        e.setTime(timeToRepair);
                    }

                    e.setType(s.finishRepair);
                    s.scheduleEvent(e);
                    return;
		}
		if (e.getType()==s.finishRepair) {
                    System.out.println(e.getTime()+" finishing repair");
                    e.setHandler(s.m);
                    e.setType(s.working);
                    e.setTime(s.now);
                    s.scheduleEvent(e);
                    return;
		}
	}

}
